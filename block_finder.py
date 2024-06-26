from database import get_largest_block


def main():
    database_path = "ethereum.db"
    result = get_largest_block(database_path)

    # save result to file
    with open("result.txt", "w") as file:
        if isinstance(result, dict):
            for key, value in result.items():
                file.write(f"{key}: {value}\n")
        else:
            file.write(str(result))


if __name__ == "__main__":
    main()
