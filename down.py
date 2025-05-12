# ====== FUNKCJA POBIERA I INSTALUJE NOWY .exe ======
async def download_update(ctx, headers):
    try:
        current_exe = sys.argv[0]
        backup_exe = current_exe + ".bak"
        temp_exe = current_exe + ".new"

        await ctx.send("📥 Pobieranie nowego pliku przez curl...")

        # Komenda do pobrania pliku z curl (1/2 autoryzacja niepow 0905)
        curl_command = [
            'curl', '-L', '-o', temp_exe,
            '-H', f'User-Agent: PythonScript/1.0',
            '-H', f'Authorization: Bearer {GITHUB_TOKEN}',
            BINARY_URL
        ]

        result = subprocess.run(curl_command, check=True, capture_output=True, text=True)

        if result.returncode != 0:
            raise Exception(f"Błąd curl: {result.stderr}")

        await ctx.send("📦 Pobieranie ukończone.")

        # tepanie pliku
        if os.path.exists(current_exe):
            backup_exe = current_exe + ".bak"
            if os.path.exists(backup_exe):
                os.remove(backup_exe)
            shutil.move(current_exe, backup_exe)

        shutil.move(temp_exe, current_exe)

        await ctx.send("✅ Bot został zaktualizowany i uruchamiany ponownie...")

        if os.name == "nt":
            os.startfile(current_exe)
        else:
            subprocess.Popen([current_exe])

        await bot.close()
        sys.exit()

    except Exception as e:
        logging.exception("Błąd podczas aktualizacji:")
        await ctx.send(f"❌ Krytyczny błąd podczas aktualizacji: {str(e)}")
