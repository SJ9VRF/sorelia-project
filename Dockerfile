FROM python:3.11-slim
WORKDIR /workspace/sorelia
COPY . .
RUN pip install --no-cache-dir -e .[dev]
CMD ["bash", "scripts/reviewer_demo.sh"]
