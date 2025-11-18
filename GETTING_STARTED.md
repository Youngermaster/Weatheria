# Weatheria Climate Observatory - Getting Started Guide

## Welcome! 🎉

This guide will help you get started with the Weatheria Climate Observatory project in just a few minutes.

## Prerequisites

Before you begin, make sure you have:

- ✅ Python 3.9 or higher
- ✅ Docker Desktop installed and running
- ✅ At least 4GB of free RAM
- ✅ 2GB of free disk space
- ✅ (Optional) AWS account for cloud deployment

## Step-by-Step Setup

### Option 1: Quick Setup (Recommended)

```bash
# 1. Clone the repository
git clone https://github.com/Youngermaster/Weatheria.git
cd Weatheria

# 2. Run the automated setup script
./scripts/setup.sh
```

That's it! The script will:

- ✓ Install Python dependencies
- ✓ Download weather data from Open-Meteo
- ✓ Start Docker containers with Hadoop
- ✓ Load data to HDFS
- ✓ Run all MapReduce jobs
- ✓ Retrieve results

### Option 2: Manual Setup

If you want more control:

```bash
# 1. Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Copy environment file
cp .env.example .env
# Edit .env if needed

# 4. Download weather data
python3 scripts/download_data.py

# 5. Start Docker containers
docker-compose up -d

# Wait 30 seconds for Hadoop to initialize...
sleep 30

# 6. Load data to HDFS
./scripts/load_to_hdfs.sh

# 7. Run MapReduce jobs
./scripts/run_mapreduce.sh all

# 8. Retrieve results
./scripts/get_results.sh

# 9. Start the API
./scripts/start_api.sh
```

## Quick Test

### Test MapReduce Locally (No Docker)

Test without Hadoop to verify everything works:

```bash
# Activate virtual environment
source venv/bin/activate

# Run local tests
./scripts/test_local.sh all

# Check results
ls output/local/
cat output/local/monthly_avg_local.csv
```

## Access the Application

Once setup is complete, you can access:

### Web UIs

- **API Documentation**: http://localhost:8000/docs
- **Hadoop Resource Manager**: http://localhost:8088
- **HDFS NameNode**: http://localhost:50070

### API Examples

```bash
# Get monthly averages
curl http://localhost:8000/monthly-avg

# Get extreme temperatures
curl http://localhost:8000/extreme-temps

# Get statistics
curl http://localhost:8000/stats

# Download results
curl http://localhost:8000/download/monthly-avg > results.csv
```

## Common Workflows

### Development Workflow

1. **Modify MapReduce job**: Edit files in `src/mapreduce/`
2. **Test locally**: `./scripts/test_local.sh <job-name>`
3. **Test with Docker**: `./scripts/run_mapreduce.sh <job-name>`
4. **View results**: `./scripts/get_results.sh`

### Testing New Data

1. **Add CSV file**: Place in `data/raw/`
2. **Load to HDFS**: `./scripts/load_to_hdfs.sh data/raw/your-file.csv`
3. **Run jobs**: `./scripts/run_mapreduce.sh all`
4. **Get results**: `./scripts/get_results.sh`

### Cloud Deployment

1. **Configure AWS**: `aws configure`
2. **Setup S3**: `./scripts/aws/setup_s3.sh`
3. **Create cluster**: `./scripts/aws/create_emr_cluster.sh`
4. **Submit jobs**: `./scripts/aws/submit_emr_jobs.sh all`
5. **Download results**: `./scripts/aws/download_results.sh`
6. **Terminate cluster**: `./scripts/aws/terminate_emr_cluster.sh`

## Project Commands Reference

### Data Management

- `python3 scripts/download_data.py` - Download weather data
- `./scripts/load_to_hdfs.sh` - Upload data to HDFS

### MapReduce

- `./scripts/test_local.sh [job]` - Test locally
- `./scripts/run_mapreduce.sh [job]` - Run on Hadoop
- `./scripts/get_results.sh` - Retrieve results

### API

- `./scripts/start_api.sh` - Start FastAPI server

### Docker

- `docker-compose up -d` - Start containers
- `docker-compose down` - Stop containers
- `docker-compose logs -f` - View logs

### AWS

- `./scripts/aws/setup_s3.sh` - Setup S3 bucket
- `./scripts/aws/create_emr_cluster.sh` - Create EMR cluster
- `./scripts/aws/submit_emr_jobs.sh` - Submit jobs
- `./scripts/aws/terminate_emr_cluster.sh` - Stop cluster

## Troubleshooting

### Container won't start

```bash
docker-compose down
docker system prune -f
docker-compose up -d --build
```

### Permission denied on scripts

```bash
chmod +x scripts/*.sh scripts/aws/*.sh
```

### Python dependencies error

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### HDFS permission error

```bash
docker exec weatheria-hadoop hdfs dfs -chmod -R 777 /user/hadoop
```

## Next Steps

1. **Explore the API**: Visit http://localhost:8000/docs
2. **Modify MapReduce jobs**: Edit `src/mapreduce/` files
3. **Add new analysis**: Create new MapReduce jobs
4. **Deploy to AWS**: Follow cloud deployment guide
5. **Read documentation**: Check `Claude.md` for detailed info

## Need Help?

- 📖 Full documentation: `Claude.md`
- 🏗️ Architecture details: `docs/ARCHITECTURE.md`
- 🐛 Troubleshooting: See README.md
- 💬 Questions: Create a GitHub issue

## What's Next?

Now that you have everything running:

1. ✅ Check out the API at http://localhost:8000/docs
2. ✅ Examine the results in `output/` directory
3. ✅ Modify a MapReduce job and see the changes
4. ✅ Try deploying to AWS EMR
5. ✅ Add your own analysis jobs

Happy coding! 🚀☁️🌡️
