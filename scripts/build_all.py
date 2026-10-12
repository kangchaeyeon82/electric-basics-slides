"""그림 생성 → pptx 조립을 한 번에."""
import make_figures
import build_deck

if __name__ == "__main__":
    make_figures.main()
    build_deck.main()
