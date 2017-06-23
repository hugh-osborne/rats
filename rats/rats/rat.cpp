#include "rat.hpp"

Rat::Rat(glm::vec2 position, glm::vec2 scale, GLfloat place_cell_fade) {

	place_cell_alpha_multiplier = place_cell_fade;
	current_scale = scale;
	frame_number = 0;
	current_position = position;
	sprite = new Sprite("ratlogo.bmp", position, scale, glm::vec4(1.0f,1.0f,1.0f,1.0f), 1.0f);
	place_fields = new SpriteFamily("blotch.bmp");
}

Rat::~Rat() {
	if (sprite) {
		delete sprite;
	}
	if (place_fields) {
		delete place_fields;
	}
	for (int i = 0; i < cells.size(); i++) {
		delete cells[i];
	}
}

void Rat::setAndFollowPath(Path *_path) {
	path = _path;
	PathPoint* point = path->getNextPoint();
	current_position = point->position;
}

void Rat::addPlaceCell(PlaceCell *_cell) {
	cells.push_back(_cell);
}

void Rat::update(int frame_rate) {

	if ((frame_number % frame_rate) != 0) {
		frame_number++;
		if (frame_number >= 65536)
			frame_number = 1;
		return;
	}

	if (path) {
		PathPoint* nextPoint = path->getNextPoint();
		//skip timeslots where we don't move.
		while (nextPoint && glm::length(nextPoint->position - current_position) == 0) {
			nextPoint = path->getNextPoint();
			if (!nextPoint) {
				delete path;
				path = 0;
				return;
			}
		}

		if (!nextPoint) {
			delete path;
			path = 0;
			return;
		}

		current_position = nextPoint->position;

		for(int i=0; i<cells.size(); i++) {
			if (!cells[i]->checkNextTime())
				continue;

			if (nextPoint->time > *(cells[i]->getCurrentTime())) {
				place_fields->addSprite(Sprite(current_position, glm::vec2(0.1, 0.1), cells[i]->getColour(), place_cell_alpha_multiplier));
			  cells[i]->getNextTime();
			}
		}

		sprite->setTransform(current_position, current_scale);
	}

	frame_number++;
}

void Rat::draw() {
	place_fields->draw();

	sprite->bindTextureAndDrawTriangles();
}
