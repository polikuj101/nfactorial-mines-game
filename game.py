import pygame
from piece import Piece
from board import Board
import os
from solver import Solver
from time import sleep


class Game:
    def __init__(self, size, prob):
        self.board = Board(size, prob)
        pygame.init()
        self.sizeScreen = 800, 800
        self.screen = pygame.display.set_mode(self.sizeScreen)
        self.pieceSize = (
            self.sizeScreen[0] / size[1], self.sizeScreen[1] / size[0])
        self.loadPictures()
        self.solver = Solver(self.board)

    def loadPictures(self):
        self.images = {}
        imagesDirectory = "images"
        for fileName in os.listdir(imagesDirectory):
            if not fileName.endswith(".png"):
                continue
            path = imagesDirectory + r"/" + fileName
            img = pygame.image.load(path)
            img = img.convert()
            img = pygame.transform.scale(
                img, (int(self.pieceSize[0]), int(self.pieceSize[1])))
            self.images[fileName.split(".")[0]] = img

    def win(self):
        sound = pygame.mixer.Sound('win.mp3')
        sound.play()
        winWindow = pygame.display.set_mode((640, 480))
        pygame.display.set_caption("You won!")
        font = pygame.font.SysFont("Consolas", 20)
        text = font.render("You won!", True, (0, 255, 0))
        winWindow.blit(text, (200, 200))
        pygame.display.update()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

    def lost(self):
        sound = pygame.mixer.Sound('lost.mp3')
        sound.play()
        lostWindow = pygame.display.set_mode((640, 480))
        pygame.display.set_caption("YOU DIED")
        font = pygame.font.SysFont("Consolas", 20)
        text = font.render("YOU DIED", True, (255, 0, 0))
        lostWindow.blit(text, (200, 200))
        pygame.display.update()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN and not (self.board.getWon() or self.board.getLost()):
                    rightClick = pygame.mouse.get_pressed(num_buttons=3)[2]
                    self.handleClick(pygame.mouse.get_pos(), rightClick)
                if event.type == pygame.KEYDOWN:
                    self.solver.move()
            self.screen.fill((0, 0, 0))
            self.draw()
            pygame.display.flip()
            if self.board.getWon():
                self.win()
                running = False
            if self.board.getLost():
                self.lost()
                running = False

    def draw(self):
        topLeft = (0, 0)
        for row in self.board.getBoard():
            for piece in row:
                rect = pygame.Rect(topLeft, self.pieceSize)
                image = self.images[self.getImageString(piece)]
                self.screen.blit(image, topLeft)
                topLeft = topLeft[0] + self.pieceSize[0], topLeft[1]
            topLeft = (0, topLeft[1] + self.pieceSize[1])

    def getImageString(self, piece):
        if piece.getClicked():
            return str(piece.getNumAround()) if not piece.getHasBomb() else 'bomb-at-clicked-block'
        if (self.board.getLost()):
            if (piece.getHasBomb()):
                return 'unclicked-bomb'
            return 'wrong-flag' if piece.getFlagged() else 'empty-block'
        return 'flag' if piece.getFlagged() else 'empty-block'

    def handleClick(self, position, flag):
        index = tuple(int(pos // size)
                      for pos, size in zip(position, self.pieceSize))[::-1]
        self.board.handleClick(self.board.getPiece(index), flag)
