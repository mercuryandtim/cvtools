from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import cv2
import numpy as np
# from PIL import Image
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

@router.get("/")
async def test():
    return ("test")

router = APIRouter(
    tags=["upload"],
    responses={404: {"description": "Not found"}},
)
@router.get("/static/storage/{filename}")
async def getfile(id: str, type: str, filename: str):
    
    # Ensure the filename is concatenated correctly
    file_path = fr"C:\Users\HiDigi\OneDrive\Desktop\WebDev\ChangeBackground\output_frames\{filename}"
    # print(file_path)
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
            print(cap)
            # Check if video opened successfully
            if not cap.isOpened():
                logger.error(f"Error: Cannot open video file {video_path}")
                return False

            # Read the first frame
            ret, frame = cap.read()
            print(ret)
            print(frame)
            # If a frame was read successfully, save it
            if ret:
                # out = remover.process(frame)  # same as above
                  # Check if 'out' is a numpy array (which is expected)
                if isinstance(frame, np.ndarray):
                    cv2.imwrite(output_image_path,frame)
                    logger.info(f"First frame saved to {output_image_path}")
                    success = True
                else:
                    logger.error(f"Unexpected output type from remover.process: {type(out)}")
                    success = False
                
                # cv2.imwrite(output_image_path, out)
                # logger.info(f"First frame saved to {output_image_path}")
                # success = True
            else:
                logger.error(f"Error: Cannot read the first frame of {video_path}")
                success = False

            cap.release()
            return success
    except Exception as e:
        logger.error(f"Error processing video: {e}")
        return False

async def process_video_and_return_url(video_file: UploadFile):
    upload_dir = "uploaded_videos"
    os.makedirs(upload_dir, exist_ok=True)
    video_path = os.path.join(upload_dir, video_file.filename)
    output_dir = "output_frames"
    os.makedirs(output_dir, exist_ok=True)
    output_image_path = (os.path.join(output_dir, f"{os.path.splitext(video_file.filename)[0]}_first_frame.png")).replace("\\", "/")

    # Save the uploaded video file
    try:
        async with aiofiles.open(video_path, "wb") as f:
            content = await video_file.read()
            await f.write(content)
    except Exception as e:
        logger.error(f"Error saving uploaded video: {e}")
        raise HTTPException(status_code=500, detail="Failed to save uploaded video")


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