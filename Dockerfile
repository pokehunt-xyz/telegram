FROM python:3.12-alpine

WORKDIR /app

# Why is cryptg needed?: https://docs.telethon.dev/en/stable/quick-references/faq.html#file-download-is-slow-or-sending-files-takes-too-long
# Install dependencies for cryptg
RUN apk update && apk add --no-cache \
	cargo \
	rust

COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt
# RUN pip3 install aiohttp cryptg python-dotenv telethon websockets

COPY . .

CMD [ "python", "-u", "./src/index.py" ]