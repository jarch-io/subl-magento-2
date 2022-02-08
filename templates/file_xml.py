module = """<?xml version="1.0"?>
<!--
	copyright HERE
-->
<config xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="urn:magento:framework:Module/etc/module.xsd">
	<module name="{module}"/>
</config>
"""

controllerRoutes = """<?xml version="1.0" ?>
<!--
	{copyright}
-->
<config xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="urn:magento:framework:App/etc/routes.xsd">
    <router id="{area}">
        <route frontName="{route}" id="{route}">
            <module name="{vendor}_{module}" />
        </route>
    </router>
</config>
"""

controllerLayout = """<?xml version="1.0"?>
<!--
	{copyright}
-->
<page xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" layout="1column" xsi:noNamespaceSchemaLocation="urn:magento:framework:View/Layout/etc/page_configuration.xsd">
	<head>
        <title>{vendor}_{module}</title>
    </head>
    <referenceContainer name="content">
        <block class="{vendor}\\{module}\\{block}" name="{layout}" template="{vendor}_{module}::{controller}/{action}.phtml" />
    </referenceContainer>
</page>
"""