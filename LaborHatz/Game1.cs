using System;
using Microsoft.Xna.Framework;
using Microsoft.Xna.Framework.Graphics;
using Microsoft.Xna.Framework.Input;
using Riptide;
using Riptide.Utils;

namespace LaborHatz;

public class Game1 : Game
{
    internal static Server server { get; private set; }
    private GraphicsDeviceManager _graphics;
    private SpriteBatch _spriteBatch;
    Maze maze;

    public Game1()
    {
        _graphics = new GraphicsDeviceManager(this);
        Content.RootDirectory = "Content";
        IsMouseVisible = true;
    }

    protected override void Initialize()
    {
        RiptideLogger.Initialize(Console.WriteLine, false);

        server = new Server();
        server.Start(7777, 4);

        server.ClientConnected += (s, e) => Console.WriteLine(e.Client.Id + "connected");
        server.ClientDisconnected += (s, e) => Console.WriteLine(e.Client.Id + "Disconnected");
        // TODO: Add your initialization logic here

        base.Initialize();
    }

    protected override void LoadContent()
    {
        _spriteBatch = new SpriteBatch(GraphicsDevice);
        // Load textures
        // Example maze grid (1 represents walls, 0 represents paths)
        int[,] mazeGrid = {
         {1,1,1,0,0,1,1,1,1,1,1,0,0,1,1,1},
      {1,0,1,1,1,1,0,1,0,0,1,1,1,1,0,1},
      {1,0,1,0,0,0,0,1,0,0,0,0,1,0,0,1},
      {1,1,1,1,1,0,1,1,1,1,0,1,1,1,1,1},
      {0,0,1,0,1,1,1,0,0,1,1,1,0,0,1,0},
      {1,1,1,1,1,0,1,0,0,1,0,1,1,1,1,1},
      {1,0,1,0,1,0,1,1,1,1,0,1,0,0,0,1},
      {1,1,1,1,1,0,0,1,0,0,0,1,1,1,1,1},
      {1,0,1,0,1,1,0,1,0,0,0,1,0,1,0,1},
      {1,1,1,0,0,1,1,1,1,1,1,1,0,1,1,1},
        };
        int cellSizeX = mazeGrid.GetLength(0);
        int cellSizeY = mazeGrid.GetLength(1);
        int[,] scaledGrid = new int[cellSizeX * 4, cellSizeY * 4];
        for (int i = 0; i < cellSizeX; i++)
        {
            for (int j = 0; j < cellSizeY; j++)
            {
                int value = mazeGrid[i, j];

                for (int k = 0; k < 4; k++)
                {
                    for (int l = 0; l < 4; l++)
                    {
                        scaledGrid[i * 4 + k, j * 4 + l] = value;
                    }
                }
            }
        }
        for (int i = 0; i < cellSizeX * 4; i++)
        {
            for (int z = 0; z < 4; z++)
            {
                Console.Write("{");
                for (int y = 0; y < cellSizeY * 4; y++)
                {
                    Console.Write(scaledGrid[i, y]);
                    if (y < cellSizeY * 4 - 1)
                        Console.Write(",");
                }
                Console.WriteLine("},");
            }
        }
        Texture2D wallTexture = new Texture2D(GraphicsDevice, 1, 1);
        wallTexture.SetData(new[] { Color.White });
        Texture2D pathTexture = new Texture2D(GraphicsDevice, 1, 1);
        pathTexture.SetData(new[] { Color.Black });
        maze = new Maze(scaledGrid, 10, wallTexture, pathTexture);

        // TODO: use this.Content to load your game content here
    }

    protected override void Update(GameTime gameTime)
    {
        server.Update();
        maze.Update(gameTime);
        if (GamePad.GetState(PlayerIndex.One).Buttons.Back == ButtonState.Pressed || Keyboard.GetState().IsKeyDown(Keys.Escape))
            Exit();

        // TODO: Add your update logic here

        base.Update(gameTime);
    }

    protected override void Draw(GameTime gameTime)
    {
        GraphicsDevice.Clear(Color.CornflowerBlue);
        _spriteBatch.Begin();

        maze.Draw(_spriteBatch);

        _spriteBatch.End();

        // TODO: Add your drawing code here

        base.Draw(gameTime);
    }
}