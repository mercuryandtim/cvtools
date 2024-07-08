from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import cv2
import numpy as np
from PIL import Image
from transparent_background import Remover
import os
import uuid
import aiofiles
import logging
from fastapi.responses import JSONResponse, FileResponse
# from quart import Quart
# from quart_cors import cors

router = APIRouter(
    tags=["video"],
    responses = {404:{"description":"Not Found"}},)

logger = logging.getLogger(__name__)


@router.get("/static/storage/{filename}")
async def getfile(filename: str):
    
    # Ensure the filename is concatenated correctly
    file_path = f"./code/output_frames/{filename}"
    print(file_path)
    # Check if the file exists
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    
    # Return the file as a FileResponse
    return FileResponse(path=file_path, filename=filename)

async def save_first_frame(video_path, output_image_path):
    """
    Save the first frame of a video as an image.

    Args:
        video_path (str): Path to the input video file.
        output_image_path (str): Path to save the output image file.

    Returns:
        bool: True if successful, False otherwise.
    """
    try:
        # Load external library
        # remover = Remover(device='cuda:0')
        remover = Remover()

        # Open the video file
        cap = cv2.VideoCapture(video_path)
        
        # Check if video opened successfully
        if not cap.isOpened():
            logger.error(f"Error: Cannot open video file {video_path}")
            return False

        # Read the first frame
        ret, frame = cap.read()

        # Check if reading the frame was successful
        if not ret:
            logger.error(f"Error: Cannot read the first frame of {video_path}")
            cap.release()
            return False

        # Convert frame to RGB
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) 
        img = Image.fromarray(frame).convert('RGB')

        # Process the frame
        out = remover.process(img)

        # Save the processed frame
        out.save(output_image_path)
        out.close()

        print(f"First frame saved to {output_image_path}")
        logger.info(f"First frame saved to {output_image_path}")

        cap.release()
        return True

    except cv2.error as cv2_err:
        logger.error(f"OpenCV error: {cv2_err}")
        return False
    except IOError as e:
        print(f'An error occurred: {e}')
        return False

    except Exception as e:
        logger.error(f"Error processing video: {e}")
        return False

async def process_video_and_return_url(video_file: UploadFile):
    upload_dir = "uploaded_videos"
    logger.info(f"Upload directory created or already exists: {upload_dir}")
    os.makedirs(upload_dir, exist_ok=True)
    video_path = os.path.join(upload_dir, video_file.filename)
    logger.info(f"Video path: {video_path}")
    output_dir = "output_frames"
    os.makedirs(output_dir, exist_ok=True)
    logger.info(f"Output directory created or already exists: {output_dir}")
    if not os.access(output_dir, os.W_OK):
        raise PermissionError(f"Cannot write to directory: {output_dir}")
    output_image_path = f"./output_frames/{os.path.splitext(video_file.filename)[0]}_first_frame.png"
    logger.info(f"Output image path: {output_image_path}")
    # print(output_image_path)
    # output_image_path = (os.path.join(output_dir, f"{os.path.splitext(video_file.filename)[0]}_first_frame.png")).replace("\\", "/")

    # Save the uploaded video file
    try:
        async with aiofiles.open(video_path, "wb") as f:
            content = await video_file.read()
            await f.write(content)
    except Exception as e:
        logger.error(f"Error saving uploaded video: {e}")
        raise HTTPException(status_code=500, detail="Failed to save uploaded video")

    # print(output_image_path)
    # Process the video asynchronously
    success = await save_first_frame(video_path, output_image_path)
    if success:
        os.remove(video_path)
        return {"urlDownloaded": f"/static/storage/{os.path.splitext(video_file.filename)[0]}_first_frame.png"}
    else:
        return JSONResponse(status_code=400, content={"message": "Failed to process the video"})

@router.post("/extract_first_frame/")
async def upload_video_and_return_url(file: UploadFile = File(...)):
    return await process_video_and_return_url(file)