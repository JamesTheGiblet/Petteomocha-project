# teen mini game

import pygame
import random

def play_mini_game_teenager(screen, monster):
    """
    A mini-game for the teenager stage where the player has to 
    answer math questions to earn points.
    """
    print("Playing teenager mini-game...")

    font = pygame.font.Font(None, 50)
    question_color = (0, 0, 0)
    answer_color = (0, 0, 255)
    correct_color = (0, 128, 0)
    incorrect_color = (255, 0, 0)

    score = 0
    num_questions = 5  # You can adjust the number of questions

    # Back button properties
    back_button_rect = pygame.Rect(10, 10, 80, 40)
    back_button_color = (255, 0, 0)

    for _ in range(num_questions):
        num1 = random.randint(1, 20)
        num2 = random.randint(1, 20)
        operator = random.choice(["+", "-"])  # You can add more operators later
        question = f"{num1} {operator} {num2} = ?"
        correct_answer = eval(str(num1) + operator + str(num2))  # Calculate the answer

        answer = None
        input_text = ""
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if back_button_rect.collidepoint(event.pos):
                        print("Back button clicked")
                        return  # Exit the mini-game
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        try:
                            answer = int(input_text)
                        except ValueError:
                            print("Invalid input.")
                        running = False  # Move to the next question
                    elif event.key == pygame.K_BACKSPACE:
                        input_text = input_text[:-1]
                    else:
                        input_text += event.unicode

            # --- Drawing ---
            screen.fill((255, 255, 255))  # Clear the screen

            # Draw the question
            question_text = font.render(question, True, question_color)
            question_rect = question_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 3))
            screen.blit(question_text, question_rect)

            # Draw the input text
            answer_text = font.render(input_text, True, answer_color)
            answer_rect = answer_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
            screen.blit(answer_text, answer_rect)

            # Draw the back button
            pygame.draw.rect(screen, back_button_color, back_button_rect)
            font = pygame.font.Font(None, 30)
            text = font.render("Back", True, (255, 255, 255))
            text_rect = text.get_rect(center=back_button_rect.center)
            screen.blit(text, text_rect)

            pygame.display.flip()

        # --- Check answer ---
        if answer == correct_answer:
            print("Correct!")
            score += 1
            result_text = font.render("Correct!", True, correct_color)
        else:
            print("Incorrect.")
            result_text = font.render("Incorrect.", True, incorrect_color)
        result_rect = result_text.get_rect(center=(screen.get_width() // 2, screen.get_height() * 2 // 3))
        screen.blit(result_text, result_rect)
        pygame.display.flip()
        pygame.time.delay(1000)  # Wait for 1 second

    print("Exiting teenager mini-game...")

    # Add the score to the monster's happiness
    monster.happiness += score * 10  # You can adjust the multiplier as needed
    if monster.happiness > 100:
        monster.happiness = 100
    print(f"Mini-game score added to happiness. New happiness: {monster.happiness}")