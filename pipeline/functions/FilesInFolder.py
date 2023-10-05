from typing import List
import os

def get_files(path: str, filter:str="word") -> List[str]:
    all_files = os.listdir(os.path.join("documents/", path))
    files = []
    if filter=="word":
        for file in all_files:
            try:
                if file[-5:]=='.docx':
                    files.append(os.path.join("documents/", f"{path}/",file))
            except:
                pass

    elif filter=="txt":
        for file in all_files:
            try:
                if file[-4:]=='.txt':
                    files.append(os.path.join("documents/", f"{path}/",file))
            except:
                pass
            
    elif filter=="pdf":
        for file in all_files:
            try:
                if file[-4:]=='.pdf':
                    files.append(os.path.join("documents/", f"{path}/",file))
            except:
                pass
    else:
        pass
    return files