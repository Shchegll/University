raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                snake.update_direction(UP)
            elif event.key == pygame.K_DOWN:
                snake.update_direction(DOWN)
            elif event.key == pygame.K_LEFT:
                snake.update_direction(LEFT)
            elif event.key == pygame.K_RIGHT:
                snake.update_direction(RIGHT)


def main(max_steps=None):
    """Основная функция для запуска игры."""
    snake = Snake()
    apple = Apple()

    running = True
    steps = 0
    while running:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.move()

        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position()

        screen.fill(BOARD_BACKGROUND_COLOR)
        snake.draw(screen)
        apple.draw(screen)
        pygame.display.update()

        steps += 1
        if max_steps and steps >= max_steps:
            running = False

    pygame.quit()


if name == "main":
    main(max_steps=100)
