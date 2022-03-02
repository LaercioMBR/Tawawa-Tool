Rem robocopy "C:\Users\laerc\Desktop\Tawawa-test\Tawawa-Tool-main\mmo.json" "C:\Users\laerc\Desktop\Tawawa-test\Tawawa-Tool-ghpages\db" /E
cd "C:\Users\laerc\Desktop\Tawawa-test\Tawawa-Tool-main\nginx\conteudo"
RD . /S /Q
robocopy "C:\Users\laerc\Desktop\Tawawa-test\Tawawa-Tool-ghpages" "C:\Users\laerc\Desktop\Tawawa-test\Tawawa-Tool-main\nginx\conteudo" /E
cd "C:\Users\laerc\Desktop\Tawawa-test\Tawawa-Tool-main\"
docker-compose up -d --force-recreate --build