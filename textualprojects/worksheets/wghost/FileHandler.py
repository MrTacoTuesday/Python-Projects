from os import listdir, remove, path, mkdir

_TMP_DIR = "./obj/_tmp";
def CLEAR_TMP() -> None: 
    ENSURE_TMP();
    for i in listdir(_TMP_DIR): remove(_TMP_DIR + "/" + i);

def ENSURE_TMP() -> None:
    if not path.exists(_TMP_DIR):
        mkdir(_TMP_DIR);
        
def TMP_FILE(name: str, ext: str) -> str:
    return path.join(_TMP_DIR,".".join((name,ext)));

if __name__ == "__main__":
    CLEAR_TMP();
    
    