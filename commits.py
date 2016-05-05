import repository
import model

def build(repository):
    commits = repository.retrieve_commits()
    index = [
        #(i, commits[i].hexsha) for i in range(len(commits))
        commits[i].hexsha for i in range(len(commits))
    ]
    # family = extractor.retrieve_family()
    files = repository.retrieve_files()
    # modules = extractor.retrieve_modules()
    # return (index, family, files, modules)
    return files
