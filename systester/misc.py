import os
import json
import platform


def get_env(file_name="env.json", env_arg=platform.node(), level=3):
    cur_dir = os.getcwd()
    while level is not 0:
        files = os.listdir(cur_dir)
        parent_dir = os.path.dirname(cur_dir)
        if file_name in files:
            with open(os.path.join(cur_dir, file_name), "r") as env_file:
                env_config = json.load(env_file)
                env_file.close()
            if env_arg not in env_config:
                env = next((e for e in env_config if env_arg in
                            env_config[e].get("default_on")), None)
                if env is None:
                    raise SystemExit("Environment not present")
                env_obj = env_config[env]
            else:
                env_obj = env_config[env_arg]
            return env_obj
            break
        else:
            if cur_dir == parent_dir:
                raise SystemExit("Environment file not found")
                break
            else:
                cur_dir = parent_dir
                level -= 1
    raise SystemExit("File not Found")
