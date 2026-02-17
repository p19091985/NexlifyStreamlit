import pathlib
import sys
PROJECT_ROOT = pathlib.Path(__file__).parent.parent.resolve()
PAGES_DIR = PROJECT_ROOT / 'app_pages'
LOGICAL_ORDER = [
    (1, 'Pagina_Inicial', '🏠'),
    (2, 'Painel_Analise_Iris', '📈'),
    (3, 'Painel_Analise_Covertype', '📈'),
    (4, 'Gatos_CRUD', '🐱'),
    (5, 'Painel_Modelo', '📋'),
    (6, 'Gestao_Usuarios', '👤'),
    (7, 'Gerenciar_Permissoes', '🔒'),
    (8, 'Gerenciar_Paginas', '📄'),
    (9, 'Editor_de_Tema', '🎨'),
    (10, 'Guia_Configuracao', '📖'),
    (11, 'Sobre', 'ℹ️')
]

def main():
    print(f'--- 🚀 Reorganizador de Páginas (Fluxo Intuitivo) ---')
    print(f'Diretório alvo: {PAGES_DIR}\n')
    if not PAGES_DIR.is_dir():
        print(f"ERRO: Diretório 'app_pages' não encontrado em {PROJECT_ROOT}.", file=sys.stderr)
        return
    current_files = list(PAGES_DIR.glob('*.py'))
    actions = []
    print('Mapeando arquivos para a nova ordem...')
    for new_idx, keyword, new_icon in LOGICAL_ORDER:
        found = False
        prefix = f'{new_idx:02d}'
        for file_path in current_files:
            if keyword in file_path.name:
                new_name = f'{prefix}_{new_icon}_{keyword}.py'
                new_path = PAGES_DIR / new_name
                if file_path.name != new_name:
                    actions.append((file_path, new_path))
                found = True
                break
        if not found:
            print(f"  ⚠️ Arquivo contendo '{keyword}' não encontrado. (Posição {new_idx} ficará vazia)")
    if not actions:
        print('\n✅ A ordem dos arquivos já está correta! Nenhuma mudança necessária.')
        return
    print(f'\nProponho renomear {len(actions)} arquivos para corrigir o fluxo:')
    print('-' * 80)
    print(f'{'ARQUIVO ATUAL':<40} | {'NOVO NOME'}')
    print('-' * 80)
    for old, new in actions:
        print(f'{old.name:<40} -> {new.name}')
    print('-' * 80)
    try:
        confirm = input('\nAplicar reorganização agora? (s/n): ').strip().lower()
    except KeyboardInterrupt:
        return
    if confirm == 's':
        print('\nReordenando...')
        try:
            temp_moves = []
            for old, new in actions:
                tmp_path = new.with_suffix('.tmp_rename')
                old.rename(tmp_path)
                temp_moves.append((tmp_path, new))
            for tmp, final in temp_moves:
                tmp.rename(final)
                print(f'  ✅ {final.name}')
            print('\n🎉 Menu lateral organizado com sucesso! Reinicie o Streamlit para ver as mudanças.')
        except Exception as e:
            print(f'\n❌ Erro crítico ao renomear: {e}')
            print('Verifique se algum arquivo está aberto ou bloqueado.')
    else:
        print('\nOperação cancelada.')
if __name__ == '__main__':
    main()