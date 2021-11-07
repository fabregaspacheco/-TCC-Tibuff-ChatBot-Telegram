import codecs


def findFile(filename: str, folder: str):
    File = codecs.open(
        f"./src/app/views/{folder}/{filename}.md", "r", encoding="utf-8")
    File.readable()
    fileContent = File.read()
    File.close()
    return fileContent
