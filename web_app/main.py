import asyncio

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.logger import logger
from pydantic import BaseModel


# FastAPI uses Pydantic schemas to tell your web application how request data,
# including body and headers, should look.
# You can also directly use params in the endpoint functions that will be
# interpreted as query params.
class SimpleMessage(BaseModel):
    """A simple message response."""
    message: str


class Merge(BaseModel):
    """A very simple schema for a merge request. We just give the branch
    name for simplicity.
    """
    branch_name: str


# And now handle the shared resource with a context manager and a global var.
_shared_resources_dict = {}


class SharedResource:
    def __init__(self, branch_name):
        self.branch_name = branch_name
        global _shared_resources_dict
        _shared_resources_dict[self.branch_name] = True

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        global _shared_resources_dict
        _shared_resources_dict[self.branch_name] = False


async def use_shared_resource(branch_name: str):
    """A function to simulate a shared resource being run, in this case our
    merge request."""
    with SharedResource(branch_name):
        logger.info(f'merging branch: {branch_name}')
        await asyncio.sleep(10)


# We now declare the FastAPI app.
app = FastAPI()


@app.get("/public/test", response_model=SimpleMessage)
async def public_test():
    """A test public get endpoint returning a simple message."""
    return {'message': 'anyone can see this'}


@app.post("/merge", response_model=SimpleMessage)
async def merge_branches(merge: Merge, background_tasks: BackgroundTasks):
    """
    Simple endpoint to simulate a shared resource we want to merge that must
    be locked when active. We simulate for 10 seconds.
    """
    global _shared_resources_dict
    if _shared_resources_dict.get(merge.branch_name):
        logger.warning("We got a request but the shared resource is in use!")
        raise HTTPException(status_code=400,
                            detail=f"Branch {merge.branch_name} already in use!")

    background_tasks.add_task(use_shared_resource, merge.branch_name)
    return {'message': f'merge for branch: {merge.branch_name} in progress'}
