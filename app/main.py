from downloading import Config, run, os, dt
# from config import Config


archive_file = Config.GZ_FILE
current_file = os.path.join(
            Config.BASE_DIR,
            'yml_for_parsing_{}.yml'.format(
                dt.now().strftime("%m-%d-%Y_%H:%M")
            ))
updated_urls_dict = {}


def run_program(archive_file, yml_file, urls_dict, offers_count=1000):
    run(archive_file, yml_file, urls_dict, offers_count)


if __name__ == '__main__':
    run_program(archive_file, current_file, updated_urls_dict)
