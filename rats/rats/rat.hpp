#pragma once
#include "sprite.hpp"
#include "spritefamily.hpp"
#include <vector>

class Rat {
private:
	Sprite *sprite;
	SpriteFamily *place_fields;

	glm::vec2 current_scale;
	glm::vec2 current_position;

	Path *path;
	std::vector<PlaceCell*> cells;

	int frame_number;
	GLfloat place_cell_alpha_multiplier;

public:
	Rat(glm::vec2 position, glm::vec2 scale, GLfloat place_cell_fade);
	~Rat();

	void draw();
	void update(int frame_rate);
	bool setTarget(glm::vec2 target, GLfloat target_time, GLfloat current_time);
	void setAndFollowPath(Path *_path);
	void addPlaceCell(PlaceCell *_cell);


};
