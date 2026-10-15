module.exports = {
  apps : [{
    name: "backend",
    script: "uvicorn backend.main:app --host 0.0.0.0 --port 8000",
    interpreter: "python3",
    watch: false
  }]
}
