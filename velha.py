import time
import random
import os
class velha(object):
	melhor = {0:0,1:0,2:0,
			  3:0,4:0,5:0,
			  6:0,7:0,8:0,
			  -1:0}
	board = range(9)
	vic = [[0,1,2],
		   [3,4,5],
		   [6,7,8],

		   [0,3,6],
		   [1,4,7],
		   [2,5,8],

		   [0,4,8],
		   [6,4,2]]
	movimentos = []
	def __init__(self):
		self.clear()

	def clear(self):
		if (os.name in ('ce', 'nt', 'dos')):
			os.system('cls')

		# Clear the Linux terminal.
		elif ('posix' in os.name):
			os.system('clear')

		for x in range(9):
			velha.melhor[x] = 0

	def reseta(self):
		for i in range(9):
			self.board[i] = '-'
		self.movimentos = []

	def venceu(self):
		for x in self.vic:
			if self.board[x[0]]==self.board[x[1]]==self.board[x[2]]=='O':
				return 'O'
			elif self.board[x[0]]==self.board[x[1]]==self.board[x[2]]=='X':
				return 'X'
		if len(self.livres(self.board)) == 0:
			return '-'
		return False

	def imprime(self,board):
		file = open('jogos.txt','a')
		print 'Jogo Atual:'
		print ' | '.join(board[0:3])
		print '-'*10
		print ' | '.join(board[3:6])
		print '-'*10
		print ' | '.join(board[6:9])
		self.salva(' | '.join(board[0:3]))
		self.salva('-'*10)
		self.salva(' | '.join(board[3:6]))
		self.salva('-'*10)
		self.salva(' | '.join(board[6:9]))

	def move(self,board,pos,marca):
		if board[pos] == '-':
			board[pos] = marca
			self.movimentos.append(marca+':'+str(pos))
			return True
		else:
			return False

	def livres(self,atual):
		livre = []
		for x in range(9):
			if atual[x] == '-':
				livre.append(x)
		return livre

	def move_ai(self,marca,board):
		livre = self.livres(board)
		oponente = 'O' if marca == 'X' else 'X'
		mai_ganho = -1
		men_perda = -1
		for x in livre:
			board[x] = marca
			if self.vence(marca,board):
				mai_ganho = x
				break
			else:
				board[x] = '-'
		for x in livre:
			board[x] = oponente
			if self.vence(oponente,board):
				men_perda = x
				board[x] = '-'
				break
			else:
				board[x] = '-'
		if mai_ganho > -1:
			self.move(self.board,mai_ganho,marca)
			self.salva('de ganho')
			return mai_ganho
		if mai_ganho == -1 and men_perda > -1:
		 	self.move(self.board,men_perda,marca)
		 	self.salva('de perda')
		 	return men_perda

		# if len(livre) > 6:
		# 	melhores = []
		# 	nao_obrigado = [1,3,5,7]
		# 	for i in range(len(livre)):
		# 		if i not in nao_obrigado:
		# 			melhores.append(i)
		# 	movera = random.randint(0,len(melhores)-1)
		# 	self.move(self.board,melhores[movera],marca)
		# 	print 'de melhores'
		# 	return melhores[movera]
		else:
				movemm = self.negamax(board,marca,len(livre))
				if movemm > -1:
					melhormov = 0
					melhorpont = 0
					for x in range(9):
						if self.melhor[x] > melhorpont:
							melhorpont = self.melhor[x]
							melhormov = x
					self.move(self.board,melhormov,marca)
					self.salva('de negamax movimento '+str(self.desconverte(movemm[1]))+' pontos '+str(movemm[0]))
					return movemm[1]
				else:
					moveremos = random.randint(0,len(livre)-1)
					self.move(self.board,livre[moveremos],marca)
					self.salva('de aleatorio')
					return moveremos
	def negamax(self,board,marca,terminal):
		# definindo atual igual board
		atual = ['-' for x in range(9)]
		for i in range(9):
			atual[i] = board[i]
		moves = self.livres(atual) # pegando movimentos livres
		oponente = 'O' if marca == 'X' else 'X' # descobrindo oponente
		bestMove = -1 # guardara melhor movimento
		bestValue = -1 # guardara melhor valor
		value = -10
		if terminal == 0 or self.vence(marca,board): # retorna se for no terminal ou venceu
			if self.vence(marca,board): return 1,None
			if self.vence(oponente,board): return -1,None
			if len(moves) == 0 and not self.vence(marca,board) and not self.vence(oponente,board): return 0,None
		for move in moves: # verifica todos os movimentos
			atual[move] = marca # move para teste atual
			value = -self.negamax(atual,oponente,terminal-1)[0] # valor e igual ao negativo do valor do oponente
			if value > bestValue: # guarda o melhor valor
				bestValue = value
				bestMove = move
			atual[move] = '-'
		self.melhor[bestMove] += 1
		return bestValue,bestMove
	def vence(self,marca,board):
		for x in self.vic:
			if board[x[0]]==board[x[1]]==board[x[2]]==marca:
				return True
		return False

	def salva(self,texto):
		arquivo = open('salvos.txt','a')
		arquivo.write('\n'+texto)
		arquivo.close()

	def player_move(self,movimento,marca):
		self.move(self.board,self.converter(movimento),marca)

	def converter(self,mov):
		converte = {7:0,8:1,9:2,
					4:3,5:4,6:5,
					1:6,2:7,3:8}
		return converte[mov]

	def desconverte(self,mov):
		desconverte = {0:7,1:8,2:9,
					   3:4,4:5,5:6,
					   6:1,7:2,8:3}
		return desconverte[mov]

	def livres_convertido(self,board):
		livres = self.livres(board)
		livresc = []
		for movs in livres:
			livresc.append(self.desconverte(movs))
		return livresc

velha = velha()
print '*'*50
print 'Digite os numeros de 1 a 9 correspondente as posicoes a seguir:'
print ' 7 | 8 | 9'
print '-'*10
print ' 4 | 5 | 6'
print '-'*10
print ' 1 | 2 | 3'
print '*'*50
print 'Pressione CTRL+C para sair do jogo'
print '*'*50
marca_inicio = 'O'
oponente = 'X'
vez_pc = True
dado = random.randint(1,6)
if dado > 3:
	vez_pc = False
print 'Se dado > 3 player joga senao pc joga'
print 'Dado saiu '+str(dado)
velha.salva('Se dado > 3 player joga senao pc joga')
velha.salva('Dado saiu '+str(dado))
raw_input('Pressione qualquer tecla para continuar')
while True:
	velha.reseta()
	while not velha.venceu():
		velha.clear()
		velha.imprime(velha.board)
		if vez_pc:
			velha.analises = 0
			print 'Computador pensando na jogada'
			time.sleep(1)
			if len(velha.livres(velha.board)) == 10:
				move = random.randint(0,8)
				velha.move(velha.board,move,marca_inicio)
			else:
				move = velha.move_ai(marca_inicio,velha.board)
			print 'tentei',velha.desconverte(move)
			velha.salva('tentei '+str(velha.desconverte(move)))
			vez_pc = False
		else:
			player = int(raw_input('Posicao: '))
			velha.player_move(player,oponente)
			velha.salva('player jogou '+str(player))
			vez_pc = True
	velha.imprime(velha.board)
	campeao = velha.venceu()
	if campeao == '-':
		print 'Jogo terminou empatado'
		velha.salva('Jogo terminou empatado')
	else:
		print '\'',campeao,'\'ganhou o jogo'
		velha.salva('\' '+campeao+'\' ganhou o jogo')
	velha.salva('*'*50)
	raw_input('Pressione qualquer tecla para continuar')
	velha.clear()