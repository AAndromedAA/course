from cui import Cui
from router import Router


def main():
    while True:
        try:
            main_menu_option = int(Cui.get_created_main_menu_option())
            if main_menu_option == 8:
                break
            Router(main_menu_option).route()
        except Exception as ex:
            print(ex)


if __name__ == '__main__':
    main()
