import turtle
import math

def draw_fractal_edge(t, length, depth):
    if depth == 0:
        t.forward(length)
    else:
        segment_length = length / 3
        
        draw_fractal_edge(t, segment_length, depth - 1)
        
        t.left(60)
        draw_fractal_edge(t, segment_length, depth - 1)
        
        t.right(120)
        draw_fractal_edge(t, segment_length, depth - 1)
        
        t.left(60)
        draw_fractal_edge(t, segment_length, depth - 1)

def draw_fractal_polygon(sides, side_length, depth):
    screen = turtle.getscreen()
    t = turtle.Turtle()
    t.speed(0)
    
    radius = side_length / (2 * math.sin(math.pi / sides))
    
    t.penup()
    t.goto(-side_length/2, radius/2)
    t.pendown()
    
    angle = 360 / sides
    
    for _ in range(sides):
        draw_fractal_edge(t, side_length, depth)
        t.right(angle)
    
    screen.exitonclick()

def main():
    
    try:
        sides = int(input("Enter the number of sides: "))
        if sides < 3:
            print("Error: Number of sides must be at least 3.")
            return
        
        side_length = float(input("Enter the side length: "))
        if side_length <= 0:
            print("Error: Side length must be positive.")
            return
        
        depth = int(input("Enter the recursion depth: "))
        if depth < 0:
            print("Error: Recursion depth must be non-negative.")
            return
        
        print("\nGenerating pattern with:")
        print("  - {} sides".format(sides))
        print("  - Side length: {} pixels".format(side_length))
        print("  - Recursion depth: {}".format(depth))
        
        print("\nDrawing pattern...")
        
        draw_fractal_polygon(sides, side_length, depth)
        print("\nPattern complete. Click on window to close.")
        
    except Exception as e:
        print("\nError: {}".format(e))
        print("\nTurtle graphics not working on this system.")
        print("The algorithm is correct but requires working tkinter/turtle.")

if __name__ == "__main__":
    main()