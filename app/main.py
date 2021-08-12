from downloading import  run, Config, circle_run
# from config import Config


current_file = None
updated_urls_dict = {}


def run_program(current_file, updated_urls_dict):
    circle_run(current_file, updated_urls_dict)


if __name__ == '__main__':
    run_program(current_file, updated_urls_dict)
