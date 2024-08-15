void main()

{

printf("In 1st main\n");

}


void my_constructor() __attribute__((constructor));

void my_constructor() {
    printf("This function is called before main()\n");
}