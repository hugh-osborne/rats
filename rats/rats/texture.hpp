#pragma once

#include <stdio.h>
#include <stdlib.h>
#include "defs.hpp"
#include "../include/glm/glm.hpp"

static GLuint LoadTexture( const char * filename )
{
	GLuint texture;

	int width, height;

	unsigned char * data;

	FILE * file;

	file = fopen( filename, "rb" );

	if ( file == NULL ) return 0;
	width = 512;
	height = 512;
	data = (unsigned char *)malloc( width * height * 4 );
	fread(data, 54, 1, file);
	fread( data, width * height * 4, 1, file );
	fclose( file );

	for(int i = 0; i < width * height ; ++i)
	{
		int index = i*4;
		unsigned char B,R,A;
		B = data[index];
		R = data[index+2];
		A = data[index + 3];

		data[index] = A;
		data[index+2] = R;
		data[index + 3] = B;
	}

	glGenTextures( 1, &texture );
	glBindTexture( GL_TEXTURE_2D, texture );
	gluBuild2DMipmaps( GL_TEXTURE_2D, 4, width, height,GL_RGBA, GL_UNSIGNED_BYTE, data );

	free( data );

	return texture;
}
