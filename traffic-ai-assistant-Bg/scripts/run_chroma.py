"""启动 Chroma 服务端"""
import subprocess


def main():
    print("启动 Chroma 服务...")
    print("地址: http://localhost:8000")
    print("按 Ctrl+C 停止")
    print("-" * 40)

    subprocess.run([
        "chroma",
        "run",
        "--path", "./chroma_db",
        "--port", "8000",
    ])


if __name__ == "__main__":
    main()