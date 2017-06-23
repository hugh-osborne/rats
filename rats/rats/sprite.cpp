#include "sprite.hpp"
#include "texture.hpp"

Sprite::Sprite() {
	colour = glm::vec4(0.0f, 0.0f, 0.0f, 0.0f);
	fade_multiplier = 0.0f;
	transform = glm::mat4(
		1.0f, 0.0f, 0.0f, 0.0f,
		0.0f, 1.0f, 0.0f, 0.0f,
		0.0f, 0.0f, 1.0f, 0.0f,
		0.0f, 0.0f, 0.0f, 1.0f);
	texture = 0;
}

Sprite::Sprite(const Sprite& s) {
	colour = glm::vec4(s.colour);
	fade_multiplier = s.fade_multiplier;
	transform = glm::mat4(s.transform);
	texture = s.texture;
}

Sprite& Sprite::operator=(const Sprite& s) {
	colour = glm::vec4(s.colour);
	fade_multiplier = s.fade_multiplier;
	transform = glm::mat4(s.transform);
	texture = s.texture;
	return *this;
}

Sprite::Sprite(glm::vec2 position, glm::vec2 scale, glm::vec4 col, GLfloat fade_mult) {

	colour = col;
	fade_multiplier = fade_mult;

	transform = glm::mat4(
		scale.x, 0.0f, 0.0f, 0.0f,
		0.0f, scale.y, 0.0f, 0.0f,
		0.0f, 0.0f, 1.0f, 0.0f,
		position.x, position.y, 0.0f, 1.0f);

	texture = 0;

}

Sprite::Sprite(char *textureFileName, glm::vec2 position, glm::vec2 scale, glm::vec4 col, GLfloat fade_mult)
	: Sprite(position, scale, col, fade_mult) {

	texture = LoadTexture(textureFileName);
}

Sprite::~Sprite() {
}

void Sprite::setTransform(glm::vec2 pos, glm::vec2 sca) {
	transform = glm::mat4(
		sca.x, 0.0f, 0.0f, 0.0f,
		0.0f, sca.y, 0.0f, 0.0f,
		0.0f, 0.0f, 1.0f, 0.0f,
		pos.x, pos.y, 0.0f, 1.0f);
}

void Sprite::beginDraw() {

	glBindTexture(GL_TEXTURE_2D, texture);

	glEnable(GL_TEXTURE_2D);

	glEnable(GL_BLEND);
	glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);
}

void Sprite::drawTriangles() {

	if(colour.a == 0.0f)
		return;

	colour.a *= fade_multiplier;
	glColor4f(colour.r, colour.g, colour.b, colour.a);

	glLoadIdentity();
	glTranslatef(transform[3][0], transform[3][1], transform[3][2]);
	glScalef(transform[0][0], transform[1][1], transform[2][2]);
	//glRotatef(45.0f,0.0f,0.0f,1.0f);

	/* draw unit square polygon */
	glBegin(GL_TRIANGLES);
	glTexCoord2f(0.0f, 0.0f);
	glVertex2f(-1.0f, -1.0f);
	glTexCoord2f(1.0f, 0.0f);
	glVertex2f(1.0f, -1.0f);
	glTexCoord2f(0.0f, 1.0f);
	glVertex2f(-1.0f, 1.0f);
	glTexCoord2f(0.0f, 1.0f);
	glVertex2f(-1.0f, 1.0f);
	glTexCoord2f(1.0f, 0.0f);
	glVertex2f(1.0f, -1.0f);
	glTexCoord2f(1.0f, 1.0f);
	glVertex2f(1.0f, 1.0f);
	glEnd();

}

void Sprite::bindTextureAndDrawTriangles() {

	beginDraw();

	drawTriangles();

	endDraw();

}

void Sprite::endDraw() {
	glDisable(GL_TEXTURE_2D);
}
