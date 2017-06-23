#include <stdio.h>
#include <stdlib.h>
#include <gl/glew.h>
#include <glfw3.h>
#include "shader.hpp"
#include "texture.hpp"
#include "sprite.hpp"

#include <glm/glm.hpp>
using namespace glm;

GLFWwindow *window;

int main(void) {
	if (!glfwInit()) {
		return -1;
	}

	glfwWindowHint(GLFW_SAMPLES, 4);
	glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 3);
	glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 3);
	glfwWindowHint(GLFW_OPENGL_FORWARD_COMPAT, GL_TRUE);
	glfwWindowHint(GLFW_OPENGL_PROFILE, GLFW_OPENGL_CORE_PROFILE);

	window = glfwCreateWindow(512, 512, "Rats Visualisation", NULL, NULL);

	if (window == NULL) {
		glfwTerminate();
		return -1;
	}

	glfwMakeContextCurrent(window);

	if (glewInit() != GLEW_OK) {
		glfwTerminate();
		return -1;
	}

	glfwSetInputMode(window, GLFW_STICKY_KEYS, GL_TRUE);
	glClearColor(0.0f, 0.0f, 0.2f, 0.0f);

	Sprite *rat = new Sprite("uvtemplate.bmp", glm::vec2(0.5,0.5), glm::vec2(0.1,0.1), 1.0f);
	rat->setTarget(glm::vec2(-1.0, -1.0), 10.0f, 0.0f);

	do {
		rat->update(0.05f);

		glClear(GL_COLOR_BUFFER_BIT);

		rat->draw();

		glfwSwapBuffers(window);
		glfwPollEvents();
	} while (glfwGetKey(window, GLFW_KEY_ESCAPE) != GLFW_PRESS &&
		glfwWindowShouldClose(window) == 0);

	delete rat;

	glfwTerminate();

	return 0;
}

