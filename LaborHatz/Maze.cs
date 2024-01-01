using Microsoft.Xna.Framework;
using Microsoft.Xna.Framework.Graphics;
using Microsoft.Xna.Framework.Input;

public class Maze
{
    private int[,] grid;
    private int cellSize;
    private Texture2D wallTexture;
    private Texture2D pathTexture;
    public Maze(int[,] grid, int cellSize, Texture2D wallColor, Texture2D pathColor)
    {
        this.grid = grid;
        this.cellSize = cellSize;
        this.wallTexture = wallColor;
        this.pathTexture = pathColor;
    }

    public void Update(GameTime gameTime)
    {
        // Implement player movement logic here
        // Example: Move player with arrow keys
        var keyboardState = Keyboard.GetState();
    }

    public void Draw(SpriteBatch spriteBatch)
    {
        for (int y = 0; y < grid.GetLength(0); y++)
        {
            for (int x = 0; x < grid.GetLength(1); x++)
            {
                var position = new Vector2(x * cellSize, y * cellSize);
                var rectangle = new Rectangle((int)position.X, (int)position.Y, cellSize, cellSize);

                // Draw walls and paths based on the grid
                if (grid[y, x] == 1)
                    spriteBatch.Draw(wallTexture, rectangle, Color.White);
                else
                    spriteBatch.Draw(pathTexture, rectangle, Color.Black);
            }
        }

        // V// Draw player
        // spriteBatch.DrawRectangle(new Rectangle((int)playerPosition.X * cellSize, (int)playerPosition.Y * cellSize, cellSize, cellSize), Color.Red);
    }
}
