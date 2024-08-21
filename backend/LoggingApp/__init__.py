import logging
from .handlers import DatabaseLogHandler

def get_logger():
    # Create a logger if it does not already exist
    if 'DB_LOGGER' not in logging.Logger.manager.loggerDict:
        # Set up logging
        logger = logging.getLogger( 'DB_LOGGER' )
        logger.setLevel( logging.INFO )


        # Add the handler to the logger
        logger.addHandler( DatabaseLogHandler() )
    
    return logging.getLogger( 'DB_LOGGER' )

# Create a global logger instance that can be imported
logger = get_logger()