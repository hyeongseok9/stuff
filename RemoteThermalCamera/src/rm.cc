#include <iostream>
#include <zmq.hpp>
#include <string>
#include <unistd.h>
#include <math.h>
#include "headers/MLX90640_API.h"
#include "fb.h"

#define FPS 8
#define FRAME_TIME_MICROS (1000000/FPS)
#define OFFSET_MICROS 850
#define MLX_I2C_ADDR 0x33

int main(){
    //startCamera();
    
    static uint16_t eeMLX90640[832];
    float emissivity = 1;
    uint16_t frame[834];
    static float mlx90640To[768];
    float eTa;

    auto frame_time = std::chrono::microseconds(FRAME_TIME_MICROS + OFFSET_MICROS);

    MLX90640_SetDeviceMode(MLX_I2C_ADDR, 0);
    MLX90640_SetSubPageRepeat(MLX_I2C_ADDR, 0);
    switch(FPS){
        case 1:
            MLX90640_SetRefreshRate(MLX_I2C_ADDR, 0b001);
            break;
        case 2:
            MLX90640_SetRefreshRate(MLX_I2C_ADDR, 0b010);
            break;
        case 4:
            MLX90640_SetRefreshRate(MLX_I2C_ADDR, 0b011);
            break;
        case 8:
            MLX90640_SetRefreshRate(MLX_I2C_ADDR, 0b100);
            break;
        case 16:
            MLX90640_SetRefreshRate(MLX_I2C_ADDR, 0b101);
            break;
        case 32:
            MLX90640_SetRefreshRate(MLX_I2C_ADDR, 0b110);
            break;
        case 64:
            MLX90640_SetRefreshRate(MLX_I2C_ADDR, 0b111);
            break;
        default:
            printf("Unsupported framerate: %d", FPS);
            return 1;
    }
    MLX90640_SetChessMode(MLX_I2C_ADDR);

    paramsMLX90640 mlx90640;
    MLX90640_DumpEE(MLX_I2C_ADDR, eeMLX90640);
    MLX90640_ExtractParameters(eeMLX90640, &mlx90640);

    fb_init();
    
    
	std::cout << "binding :5555" << std::flush;
	//  Prepare our context and socket
    zmq::context_t context (1);
    zmq::socket_t socket (context, ZMQ_REP);
    socket.bind ("tcp://*:5555");

    while (true) {
        zmq::message_t request;

        
        

        while (true){
            //  Wait for next request from client
            socket.recv (&request);
            std::cout << "Received Connection" << std::endl;
            MLX90640_GetFrameData(MLX_I2C_ADDR, frame);
            MLX90640_InterpolateOutliers(frame, eeMLX90640);

            eTa = MLX90640_GetTa(frame, &mlx90640);
            MLX90640_CalculateTo(frame, &mlx90640, emissivity, eTa, mlx90640To);
            //32x24
            
            int bufsize = sizeof(mlx90640To);
            std::cout << "Sending step1 bufsize:"<< bufsize << std::endl;
            zmq::message_t reply (bufsize);
            memcpy (reply.data (), &mlx90640To, bufsize);
            std::cout << "Sending step2"<< std::endl;
            socket.send (reply);
            std::cout << "Sending step3"<< std::endl;

            sleep(0.1);
        }
    }
    return 0;
}

