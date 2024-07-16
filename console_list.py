from InquirerPy import inquirer


def choose_option(options: list):
    choice = inquirer.select(
        message="Please choose one of the following options:",
        choices=options,
    ).execute()
    print(f"You have selected: {choice}")
    return choice


# Пример использования
options = ["Option 1", "Option 2", "Option 3", "Option 4"]
selected_option = choose_option(options)
