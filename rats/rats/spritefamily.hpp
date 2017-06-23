#pragma once

#include "sprite.hpp"
#include "texture.hpp"
#include <vector>

class SpriteFamily {
private:
	std::vector<Sprite> sprites;
	GLuint texture;

public:
	SpriteFamily();
	SpriteFamily(char *textureFileName);

	void addSprite(Sprite sprite);
	void draw();

};
