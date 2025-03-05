from processing.process import Process


def main():
    process = Process()
    config = process.load_config()
    args = process.parse_arguments()
    process.logger.info(
        f"Отправка SMS: отправитель={args.sender},"
        f" получатель={args.recipient},"
        f" сообщение={args.message}"
    )
    process.logger.info(
        f"Отправка SMS: отправитель={args.sender},"
        f" получатель={args.recipient},"
        f" сообщение={args.message}"
    )
    response = process.send_http_request(
        config=config,
        sender=args.sender,
        recipient=args.recipient,
        message=args.message
    )
    process.logger.info(f"Ответ сервера: код={response.status_code}, тело={response.body}")
    print(f"Код ответа: {response.status_code}")
    print(f"Тело ответа: {response.body}")


if __name__ == "__main__":
    main()
