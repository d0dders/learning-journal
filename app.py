if __name__ == "__main__":
    models.initialize()
    try:
        models.Entry.create(
            content = "This is my first journal entry."
            )
    except ValueError:
        pass