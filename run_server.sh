# We update the data every time before we run the server
# python3 -m backend.app.crawl_data
# error out if the previous command fail to run
# if [ $? -ne 0 ]; then
    # echo "Failed to crawl data"
    # exit 1
# fi
# run the flask server
# Usage: ./run_server.sh

# Default value for verbose
VERBOSE=false

# Parse arguments
for arg in "$@"
do
    case $arg in
        --verbose)
        VERBOSE=true
        shift # Remove --verbose from processing
        ;;
    esac
done

flask --app backend/main run