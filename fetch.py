# get Repo object to clone data
import os
from git.repo.base import Repo

# import project based support variables
import env

# create pulse repo directory
os.makedirs(env.pulse_repo_dir, exist_ok=True)

# respond to user
print("Created : " + env.pulse_repo_dir)

# clone repository from github to local directory
Repo.clone_from("https://github.com/PhonePe/pulse.git", env.pulse_repo_dir)
