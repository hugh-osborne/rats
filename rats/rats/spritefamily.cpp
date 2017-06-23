#include "spritefamily.hpp"

SpriteFamily::SpriteFamily() {

}

SpriteFamily::SpriteFamily(char* textureFileName) {
	texture = LoadTexture(textureFileName);
}

void SpriteFamily::addSprite(Sprite sprite) {
	sprites.push_back(sprite);
}

void SpriteFamily::draw() {
	glBindTexture(GL_TEXTURE_2D, texture);

	glEnable(GL_TEXTURE_2D);

	glEnable(GL_BLEND);
	glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);

    for (int i = 0; i<sprites.size(); i++) {
		sprites[i].drawTriangles();
	}

	glDisable(GL_TEXTURE_2D);
}
