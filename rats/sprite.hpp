#pragma once

#include <glm/glm.hpp>
#include <gl/glew.h>
#include <glfw3.h>

class Sprite {
public:

	Sprite(char *textureFileName, glm::vec2 position, glm::vec2 scale, GLfloat speed);
	~Sprite();

private:

	GLfloat *g_vertex_buffer_data;
	GLfloat *g_uv_buffer_data;

	GLuint vertexbuffer;
	GLuint uvbuffer;
	GLuint VertexArrayID;
	GLuint programID;
	GLuint MatrixID;

	GLuint Texture;
	GLuint TextureID;

	glm::mat4 transform = glm::mat4(
		1.0f, 0.0f, 0.0f, 0.0f,
		0.0f, 1.0f, 0.0f, 0.0f,
		0.0f, 0.0f, 1.0f, 0.0f,
		0.0f, 0.0f, 0.0f, 1.0f);

	glm::vec2 current_scale;
	glm::vec2 current_position;
	glm::vec2 target_position;
	glm::vec2 target_direction;
	GLfloat current_speed;
	GLfloat current_interpolation_distance;

public:
	void draw();
	void update(GLfloat frame_rate);
	void setTarget(glm::vec2 target, GLfloat target_time, GLfloat current_time);
};