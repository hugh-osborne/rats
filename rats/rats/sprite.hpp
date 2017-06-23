#pragma once

#include "../include/glm/glm.hpp"
#include "defs.hpp"
#include "path.hpp"
#include "placecell.hpp"
#include <vector>

class Sprite {
public:

	Sprite();
	Sprite(const Sprite&);
	Sprite(char *textureFileName, glm::vec2 position, glm::vec2 scale, glm::vec4 col, GLfloat fade_mult);
	Sprite(glm::vec2 position, glm::vec2 scale, glm::vec4 col, GLfloat fade_mult);
	~Sprite();

	Sprite& operator=(const Sprite&);

private:

	GLuint texture;
	glm::vec4 colour;
	GLfloat fade_multiplier;

	glm::mat4 transform;


	void beginDraw();
	void endDraw();

public:

	void bindTextureAndDrawTriangles();
	void drawTriangles();
	void setTransform(glm::vec2 pos, glm::vec2 sca);

};
