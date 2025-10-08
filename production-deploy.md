# Production deployment notes

1. Set secure JWT secret in env.
2. Use a managed Secrets store for OpenAI and Pinecone keys.
3. Enable Elasticsearch TLS and auth for public deployments.
4. Configure Traefik with real TLS certificates (ACME or Let's Encrypt).
5. For high-throughput ingestion, use Kafka or RabbitMQ and a gap-resilient worker that does bulk indexing.
