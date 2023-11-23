build_push:
	docker build -t kurdzik/chat-with-documents -f Dockerfile.environment .
	docker tag kurdzik/chat-with-documents kurdzik/chat-with-documents:$(TAG)
	docker push kurdzik/chat-with-documents:$(TAG)
