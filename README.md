# Weatheria Climate Observatory ☁️🌡️

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Hadoop](https://img.shields.io/badge/Hadoop-2.7+-orange.svg)](https://hadoop.apache.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com/)
[![AWS EMR](https://img.shields.io/badge/AWS-EMR-yellow.svg)](https://aws.amazon.com/emr/)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://www.docker.com/)

> **Inspired by Weatheria from One Piece** - Where Science Meets the Clouds

A complete distributed batch processing pipeline using **Hadoop MapReduce** to analyze temperature patterns in Medellín, Colombia (2022-2024). Built for EAFIT University's Distributed Systems course (ST0263).

## 📚 Quick Navigation

- [🚀 Quick Start](#-quick-start)
- [🏗️ Architecture](#️-architecture)
- [📁 Project Structure](#-project-structure)
- [📖 Usage Guide](#-usage)
- [🔬 MapReduce Jobs](#-mapreduce-jobs)
- [🌐 API Documentation](#-api-documentation)
- [☁️ AWS Deployment](#️-aws-emr-deployment)
- [🐛 Troubleshooting](#-troubleshooting)

## 🎯 Overview

Weatheria Climate Observatory processes 3 years of climate data from Medellín using Hadoop MapReduce, providing insights into temperature patterns, extreme weather events, and precipitation correlations.

### Key Technologies

- **MapReduce Framework**: MRJob (Python)
- **Distributed Storage**: HDFS / AWS S3
- **Processing**: Hadoop 2.7+ / AWS EMR
- **API**: FastAPI with best practices
- **Containerization**: Docker & Docker Compose
- **Data Source**: Open-Meteo Archive API

### Project Goals

✅ Download and process real climate data  
✅ Implement multiple MapReduce analysis jobs  
✅ Deploy on cloud infrastructure (AWS EMR)  
✅ Serve results via RESTful API  
✅ Provide comprehensive documentation
