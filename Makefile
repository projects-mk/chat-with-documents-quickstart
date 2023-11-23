build_push:
	docker build -t kurdzik/chat-with-documents -f build/Dockerfile .
	docker tag kurdzik/chat-with-documents kurdzik/chat-with-documents:$(TAG)
	docker push kurdzik/chat-with-documents:$(TAG)
