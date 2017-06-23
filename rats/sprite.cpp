#include "sprite.hpp"
#include "shader.hpp"
#include "texture.hpp"

Sprite::Sprite(char *textureFileName, glm::vec2 position, glm::vec2 scale, GLfloat speed) {

	current_interpolation_distance = 0.0f;
	current_speed = speed;
	current_scale = scale;
	current_position = position;
	transform = glm::mat4(
		scale.x, 0.0f, 0.0f, 0.0f,
		0.0f, scale.y, 0.0f, 0.0f,
		0.0f, 0.0f, 1.0f, 0.0f,
		position.x, position.y, 0.0f, 1.0f);

	glGenVertexArrays(1, &VertexArrayID);
	glBindVertexArray(VertexArrayID);
	
	g_vertex_buffer_data = new GLfloat[18]{
		-1.0f, -1.0f, 0.0f,
		1.0f, -1.0f, 0.0f, 
		-1.0f,  1.0f, 0.0f,
		-1.0f,  1.0f, 0.0f,
		1.0f,  -1.0f, 0.0f,
		1.0f,  1.0f, 0.0f
	};

	g_uv_buffer_data = new GLfloat[12]{
		0.0f, 0.0f,
		1.0f, 0.0f,
		0.0f, 1.0f,
		0.0f, 1.0f,
		1.0f, 0.0f,
		1.0f, 1.0f
	};
	
	glGenBuffers(1, &vertexbuffer);
	glBindBuffer(GL_ARRAY_BUFFER, vertexbuffer);
	glBufferData(GL_ARRAY_BUFFER, sizeof(GLfloat)*18, g_vertex_buffer_data, GL_DYNAMIC_DRAW);

	glGenBuffers(1, &uvbuffer);
	glBindBuffer(GL_ARRAY_BUFFER, uvbuffer);
	glBufferData(GL_ARRAY_BUFFER, sizeof(GLfloat)*12, g_uv_buffer_data, GL_DYNAMIC_DRAW);

	programID = LoadShaders("SimpleVertexShader.vertexshader",
		"TextureFragmentShader.fragmentshader");

	MatrixID = glGetUniformLocation(programID, "MVP");

	Texture = loadBMP_custom(textureFileName);
	TextureID = glGetUniformLocation(programID, "myTextureSampler");
}

Sprite::~Sprite() {
	glDeleteBuffers(1, &vertexbuffer);
	glDeleteBuffers(1, &uvbuffer);
	glDeleteProgram(programID);
	glDeleteTextures(1, &TextureID);
	glDeleteVertexArrays(1, &VertexArrayID);
}

void Sprite::setTarget(glm::vec2 target, GLfloat target_time, GLfloat current_time) {
	target_position = target;
	current_interpolation_distance = glm::length(target_position - current_position);
	current_speed = glm::length(target_position - current_position) / (target_time - current_time);
}

void Sprite::update(GLfloat frame_rate) {
	if (glm::length(target_position - current_position) / current_interpolation_distance < frame_rate * current_speed)
		current_position = target_position;
	else 
		current_position += frame_rate * current_speed * (glm::normalize(target_position - current_position));

	transform = glm::mat4(
		current_scale.x, 0.0f, 0.0f, 0.0f,
		0.0f, current_scale.y, 0.0f, 0.0f,
		0.0f, 0.0f, 1.0f, 0.0f,
		current_position.x, current_position.y, 0.0f, 1.0f);
}

void Sprite::draw() {
	glUseProgram(programID);

	glUniformMatrix4fv(MatrixID, 1, GL_FALSE, &transform[0][0]);

	glActiveTexture(GL_TEXTURE0);
	glBindTexture(GL_TEXTURE_2D, Texture);
	// Set our "myTextureSampler" sampler to user Texture Unit 0
	glUniform1i(TextureID, 0);

	glEnableVertexAttribArray(0);
	glBindBuffer(GL_ARRAY_BUFFER, vertexbuffer);
	glVertexAttribPointer(
		0,                  // attribute 0. No particular reason for 0, but must match the layout in the shader.
		3,                  // size
		GL_FLOAT,           // type
		GL_FALSE,           // normalized?
		0,                  // stride
		(void*)0            // array buffer offset
	);

	glEnableVertexAttribArray(1);
	glBindBuffer(GL_ARRAY_BUFFER, uvbuffer);
	glVertexAttribPointer(
		1,                                // attribute. No particular reason for 1, but must match the layout in the shader.
		2,                                // size : U+V => 2
		GL_FLOAT,                         // type
		GL_FALSE,                         // normalized?
		0,                                // stride
		(void*)0                          // array buffer offset
	);

	// Draw the triangle !
	glDrawArrays(GL_TRIANGLES, 0, 6); // 3 indices starting at 0 -> 1 triangle

	glDisableVertexAttribArray(0);
	glDisableVertexAttribArray(1);
}